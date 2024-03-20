import { useEffect } from 'react';
import { useAudioRecorder } from 'react-audio-voice-recorder';
import { Button } from 'react-bootstrap';
  
  export default function Recorder ()
  {
    const {
      startRecording,
      stopRecording,
      //togglePauseResume,
      recordingBlob,
      isRecording,
      //isPaused,
      //recordingTime,
      //mediaRecorder
    } = useAudioRecorder();
  
    useEffect(() => {
      if (!recordingBlob) return;
  
      // recordingBlob will be present at this point after 'stopRecording' has been called
    }, [recordingBlob])

    return (
      <div>
        { !isRecording ?
        <div>
          <p>Press start to record the audio</p><Button onClick = {startRecording}>Start</Button>
        </div> :
        <div>
          <p className="fade-in-fade-out">Recording...</p>
          <Button variant='danger' onClick = {stopRecording}>Stop</Button>
        </div> }
      </div>
    )
  }