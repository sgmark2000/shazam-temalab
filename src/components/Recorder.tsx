import { IMediaRecorder, MediaRecorder, register } from 'extendable-media-recorder';
import { connect } from 'extendable-media-recorder-wav-encoder';
import { useState } from 'react';
import Button from 'react-bootstrap/esm/Button';

let mediaRecorder: IMediaRecorder | null = null;
let audioBlobs: BlobPart[] | undefined = [];
let capturedStream: MediaStream | null = null;

register(await connect());

function startRecording() {
  return navigator.mediaDevices.getUserMedia({
    audio: {
      echoCancellation: true,
    }
  }).then(stream => {
      audioBlobs = [];
      capturedStream = stream;

      mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/wav'
      });

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

/*function playAudio(audioBlob: Blob | MediaSource) {
  if (audioBlob) {
    const audio = new Audio();
    audio.src = URL.createObjectURL(audioBlob);
    audio.play();
  }
}*/


async function uploadBlob(audioBlob: Blob) {
  const formData = new FormData();
  formData.append('audio_data', audioBlob, 'file');
  formData.append('type','wav');

  const apiUrl = "http://localhost:5000/zene";

  const response = await fetch(apiUrl, {
    method: 'POST',
    cache: 'no-cache',
    body: formData
  });

  return response.json();
}

export default function Recorder ()
{
  const [isRecording, setIsRecording] = useState(false)
  const [data, setData] = useState(null);

  function startRec()
  {
    startRecording();
    setIsRecording(true);
    setData(null);
  }

  async function stopRec()
  {
    const wavAudioBlob = await stopRecording();
    stopRecording();
    setIsRecording(false);
    if(wavAudioBlob)
      uploadBlob(wavAudioBlob);
      handleClick();  
  }

function handleClick() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://localhost:5000/site');
    xhr.onload = function() {
      if (xhr.status === 200) {
        setData(JSON.parse(xhr.responseText)["0"]);
      }
    };
    xhr.send();
    //banán
  }

  return (
    <div>
      { !isRecording ?
      <div>
        <p>Press start to record the audio</p><Button onClick = {startRec}>Start</Button>
        <div>
        {data ? <div>{data}</div> : <div></div>}
      </div>
      </div> :
      <div>
        <p className="fade-in-fade-out">Recording...</p>
        <Button variant='danger' onClick = {stopRec}>Stop</Button>
      </div> }
    </div>
  )
}
