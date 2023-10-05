# import wave
# from vosk import Model, KaldiRecognizer, SetLogLevel
# import json
# import whisper

'''
def convert(source):
    # Open audio file
    wf = wave.open(source, 'rb')

    model = Model('../../res/models/vosk-model-small-en-us-0.15')
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # To store our results
    transcription = []
    result = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            # Convert json output to dict
            result_dict = json.loads(rec.Result())
            # Extract text values and append them to transcription list
            transcription.append(result_dict.get("text", ""))
            # Append the results to the results list
            result.extend(result_dict.get("result"))

    # Get final bits of audio and flush the pipeline
    print('Result', result)
    final_result = json.loads(rec.FinalResult())
    transcription.append(final_result.get("text", ""))
    print('Final result', final_result)
    if final_result.get('result') is not None:
        result.extend(final_result.get("result"))

    # merge or join all list elements to one big string
    transcription_text = ' '.join(transcription)
    return result
 '''

def convertWithOpenAI(source):
    # model = whisper.load_model("../../res/models/tiny.en.pt")
    # result = model.transcribe("../../res/audio/complaint.mp3")
    result = {}
    result['text']="Good morning sir. I bought a phone from your shop a few days back but the camera quality is very poor. It is blurry when I take photos. The battery is also getting drained fast. I dont know how to fix this, please help me."
    print(result)
    return result