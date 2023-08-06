"""Provide JobCaching class"""
import shutil
from pathlib import Path

import toml
from diot import Diot
from xqute.utils import a_read_text, a_write_text, asyncify

from .defaults import ProcInputType, ProcOutputType
from .utils import get_mtime

class JobCaching:
    """Provide caching functionality of jobs"""

    @property
    def signature_file(self) -> Path:
        """Get the path to the signature file"""
        return self.metadir / 'job.signature.toml'

    async def cache(self) -> None:
        """write signature to signature file"""
        try:
            max_mtime = self.script_file.stat().st_mtime
        except FileNotFoundError:
            max_mtime = 0
        for inkey, intype in self.proc.input.type.items():
            if intype == ProcInputType.VAR:
                continue
            if intype == ProcInputType.FILE and self.input[inkey] is not None:
                max_mtime = max(
                    max_mtime,
                    get_mtime(self.input[inkey], self.proc.dirsig)
                )
            if intype == ProcInputType.FILES:
                for file in (self.input[inkey] or ()):
                    max_mtime = max(
                        max_mtime,
                        get_mtime(file, self.proc.dirsig)
                    )

        for outkey, outval in self._output_types.items():
            if outval == ProcOutputType.FILE:
                max_mtime = max(
                    max_mtime,
                    get_mtime(self.output[outkey], self.proc.dirsig)
                )

        signature = {
            'input': {
                'type': self.proc.input.type,
                'data': self.input,
            },
            'output': {
                'type': self._output_types,
                'data': self.output
            },
            'ctime': float('inf') if max_mtime == 0 else max_mtime
        }
        sign_str = toml.dumps(signature)
        await a_write_text(self.signature_file, sign_str)

    async def _clear_output(self) -> None:
        """Clear output if not cached"""
        self.log('debug', 'Clearing previous output files.')
        for outkey, outval in self._output_types.items():
            if outval != ProcOutputType.FILE:
                continue

            outfile = Path(self.output[outkey])
            # dead link
            if not outfile.exists():
                if outfile.is_symlink():
                    await asyncify(Path.unlink)(outfile, )
            elif not outfile.is_dir():
                await asyncify(Path.unlink)(outfile, )
            else:
                await asyncify(shutil.rmtree)(outfile)

    async def _check_cached(self) -> bool:
        """Check if the job is cached based on signature"""
        sign_str = await a_read_text(self.signature_file)
        signature = Diot(toml.loads(sign_str))

        try:
            # check if inputs/outputs are still the same
            if (signature.input.type != self.proc.input.type or
                    signature.input.data != {
                        key: val for key, val in self.input.items()
                        if val is not None
                    } or
                    signature.output.type != self._output_types or
                    signature.output.data != self.output):
                self.log(
                    'debug',
                    'Not cached (input or output is different)'
                )
                return False

            # check if any script file is newer
            if self.script_file.stat().st_mtime > signature.ctime + 1e-3:
                self.log(
                    'debug',
                    'Not cached (script file is newer: %s > %s)',
                    self.script_file.stat().st_mtime,
                    signature.ctime
                )
                return False

            for inkey, intype in self.proc.input.type.items():
                if intype == ProcInputType.VAR or self.input[inkey] is None:
                    continue
                if intype == ProcInputType.FILE:
                    if get_mtime(
                            self.input[inkey],
                            self.proc.dirsig
                    ) > signature.ctime + 1e-3:
                        self.log(
                            'debug',
                            'Not cached (Input file is newer: %s)',
                            inkey
                        )
                        return False
                if intype == ProcInputType.FILES:
                    for file in self.input[inkey]:
                        if get_mtime(
                                file,
                                self.proc.dirsig
                        ) > signature.ctime + 1e-3:
                            self.log(
                                'debug',
                                'Not cached (One of the input files '
                                'is newer: %s)',
                                inkey
                            )
                            return False

            for outkey, outval in self._output_types.items():
                if outval != ProcOutputType.FILE:
                    continue
                if get_mtime(
                        self.output[outkey],
                        self.proc.dirsig
                ) > signature.ctime + 1.0e-3:
                    self.log(
                        'debug',
                        'Not cached (Output file is newer: %s)',
                        outkey
                    )
                    return False

        except (AttributeError, FileNotFoundError): # pragma: no cover
            # meaning signature is incomplete
            # or any file is deleted
            return False
        return True

    @property
    async def cached(self) -> bool: # pylint: disable=too-many-branches
        """check if a job is cached"""
        out = True
        if (not self.proc.cache or
                await self.rc != 0 or
                not self.signature_file.is_file()):
            self.log('debug',
                     'Not cached (proc.cache=False or job.rc!=0 or '
                     'signature file not found)')
            out = False

        elif self.proc.cache == 'force':
            await self.cache()
            out = True

        else:
            out = await self._check_cached()

        if not out:
            await self._clear_output()

        return out
