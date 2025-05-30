import pytest
from pathlib import Path
from cloud_splitter.processor import Processor, ProcessingResult, SeparatorType
from unittest.mock import patch, MagicMock

@pytest.fixture
def sample_config(temp_dir):
    class Config:
        class Processing:
            separator = "demucs"
            stems = ["vocals", "drums", "bass", "other"]
        
        class Demucs:
            model = "htdemucs"
            cpu_only = True
            shifts = 2
        
        class Paths:
            output_dir = temp_dir / "output"
        
        processing = Processing()
        demucs = Demucs()
        paths = Paths()
    
    return Config()

@pytest.fixture
def processor(sample_config):
    return Processor(sample_config)

def test_processor_initialization(processor):
    assert processor.config is not None
    assert processor.device == "cpu"  # Since cpu_only is True in sample_config

@pytest.mark.asyncio
async def test_process_file_demucs(processor, temp_dir):
    input_file = temp_dir / "test.wav"
    input_file.touch()
    
    with patch('demucs.separate.main') as mock_demucs:
        # Create expected output structure
        output_dir = processor.config.paths.output_dir / input_file.stem
        output_dir.mkdir(parents=True)
        model_dir = output_dir / processor.config.demucs.model
        model_dir.mkdir()
        
        # Create mock stem directories and files
        for stem in processor.config.processing.stems:
            stem_dir = model_dir / stem
            stem_dir.mkdir()
            (stem_dir / input_file.stem).touch()
        
        result = await processor.process_file(input_file)
        
        assert isinstance(result, ProcessingResult)
        assert result.separator_used == SeparatorType.DEMUCS
        assert len(result.stems) == len(processor.config.processing.stems)
        assert all(stem in result.stems for stem in processor.config.processing.stems)

@pytest.mark.asyncio
async def test_process_file_invalid_separator(processor):
    processor.config.processing.separator = "invalid"
    input_file = Path("test.wav")
    
    with pytest.raises(ValueError, match="Unsupported separator"):
        await processor.process_file(input_file)
