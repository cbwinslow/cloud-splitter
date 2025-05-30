from pathlib import Path
from typing import List, Dict, Optional
import subprocess
from enum import Enum
import demucs.separate
import numpy as np
import torch
from pydantic import BaseModel

class SeparatorType(str, Enum):
    DEMUCS = "demucs"
    SPLEETER = "spleeter"

class ProcessingResult(BaseModel):
    input_file: Path
    output_dir: Path
    stems: Dict[str, Path]
    separator_used: SeparatorType

class Processor:
    def __init__(self, config):
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() and not config.demucs.cpu_only else "cpu"

    async def process_file(self, input_file: Path) -> ProcessingResult:
        separator = self.config.processing.separator.lower()
        if separator == SeparatorType.DEMUCS:
            return await self._process_demucs(input_file)
        elif separator == SeparatorType.SPLEETER:
            return await self._process_spleeter(input_file)
        else:
            raise ValueError(f"Unsupported separator: {separator}")

    async def _process_demucs(self, input_file: Path) -> ProcessingResult:
        output_dir = self.config.paths.output_dir / input_file.stem
        output_dir.mkdir(parents=True, exist_ok=True)

        # Prepare demucs arguments
        args = [
            str(input_file),
            "-n", self.config.demucs.model,
            "--shifts", str(self.config.demucs.shifts),
            "--out", str(output_dir)
        ]

        if self.device == "cpu":
            args.append("--device=cpu")

        try:
            demucs.separate.main(args)
            
            # Collect stem paths
            stems = {}
            for stem in self.config.processing.stems:
                stem_path = output_dir / self.config.demucs.model / stem / input_file.stem
                if stem_path.exists():
                    stems[stem] = stem_path

            return ProcessingResult(
                input_file=input_file,
                output_dir=output_dir,
                stems=stems,
                separator_used=SeparatorType.DEMUCS
            )
        except Exception as e:
            raise RuntimeError(f"Demucs processing failed: {str(e)}")

    async def _process_spleeter(self, input_file: Path) -> ProcessingResult:
        # Implementation for Spleeter
        # TODO: Implement Spleeter processing
        pass
