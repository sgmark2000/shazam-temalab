import {IMediaRecorder, MediaRecorder, register} from 'extendable-media-recorder';
import {connect} from 'extendable-media-recorder-wav-encoder';
import { useState } from 'react';
import Button from 'react-bootstrap/esm/Button';

let mediaRecorder: IMediaRecorder | null = null;
let audioBlobs: BlobPart[] | undefined = [];
let capturedStream: MediaStream | null = null;

// Register the extendable-media-recorder-wav-encoder
register(await connect());

//async connect() {
//  await register(await connect());
//}

// Starts recording audio
function startRecording() {
  return navigator.mediaDevices.getUserMedia({
    audio: {
      echoCancellation: true,
    }
  }).then(stream => {
      audioBlobs = [];
      capturedStream = stream;

      // Use the extended MediaRecorder library
      mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/wav'
      });

      // Add audio blobs while recording 
      mediaRecorder.addEventListener('dataavailable', event => {
        if (audioBlobs != undefined)
          audioBlobs.push(event.data);
      });

      mediaRecorder.start();
  }).catch((e) => {
    console.error(e);
  });

}

function stopRecording() {
  return new Promise<Blob | null>(resolve => {
    if (!mediaRecorder) {
      resolve(null);
      return;
    }

    mediaRecorder.addEventListener('stop', () => {
      let mimeType = ""

      if (mediaRecorder)
        mimeType = mediaRecorder.mimeType;

      const audioBlob = new Blob(audioBlobs, { type: mimeType });

      if (capturedStream) {
        capturedStream.getTracks().forEach(track => track.stop());
      }

      resolve(audioBlob);
    });
    
    mediaRecorder.stop();
    
  });
}

function playAudio(audioBlob: Blob | MediaSource) {
  if (audioBlob) {
    const audio = new Audio();
    audio.src = URL.createObjectURL(audioBlob);
    audio.play();
  }
}

export default function Recorder ()
{
  const [isRecording, setIsRecording] = useState(false)
  function startRec()
  {
    startRecording();
    setIsRecording(true);
  }

  async function stopRec()
  {
    //stopRecording();
    const wavAudioBlob = await stopRecording();
    stopRecording();
    setIsRecording(false);
    if(wavAudioBlob)
      playAudio(wavAudioBlob);
    
  }

  return (
    <div>
      { !isRecording ?
      <div>
        <p>Press start to record the audio</p><Button onClick = {startRec}>Start</Button>
      </div> :
      <div>
        <p className="fade-in-fade-out">Recording...</p>
        <Button variant='danger' onClick = {stopRec}>Stop</Button>
      </div> }
    </div>
  )
}