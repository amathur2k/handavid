import argparse
import json
from pathlib import Path
from faster_whisper import WhisperModel

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()
model = WhisperModel('small', device='cpu', compute_type='int8')
segments, info = model.transcribe(args.input, beam_size=5, word_timestamps=True, vad_filter=True)
result = {'language': info.language, 'language_probability': info.language_probability, 'segments': [], 'words': []}
for segment in segments:
    item = {'start': segment.start, 'end': segment.end, 'text': segment.text}
    result['segments'].append(item)
    print(f'{segment.start:.2f}-{segment.end:.2f}: {segment.text}', flush=True)
    for word in segment.words or []:
        result['words'].append({'text': word.word.strip(), 'start': word.start, 'end': word.end, 'probability': word.probability})
Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print('Saved transcript:', args.output, flush=True)
