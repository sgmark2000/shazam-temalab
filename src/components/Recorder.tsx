import { AudioRecorder, useAudioRecorder } from 'react-audio-voice-recorder';
import Button from "react-bootstrap/esm/Button";

export default function Recorder() {
    const recorderControls = useAudioRecorder(
      {
        noiseSuppression: true,
        echoCancellation: true,
      },
      (err: any) => console.table(err)
    );
    const addAudioElement = (blob: Blob | MediaSource) => {
      const url = URL.createObjectURL(blob);
      const audio = document.createElement('audio');
      audio.src = url;
      audio.controls = true;
      //document.body.appendChild(audio);
    };
  
    return (
      <div>
        <AudioRecorder
          onRecordingComplete={(blob) => addAudioElement(blob)}
          recorderControls={recorderControls}
          showVisualizer={true}
        />
        <br />
        <Button onClick={recorderControls.stopRecording}>Stop recording</Button>
        <br />
      </div>
    );
  }



