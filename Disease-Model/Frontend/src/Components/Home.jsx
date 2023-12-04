import React, { useState, useRef }  from 'react'
import { BASE_URL } from '../Constants/Backend_Api';
import "./home.css"

const Home = () => {

  const api_base_url = BASE_URL;
  const fileInputRef = useRef(null); // Create a ref for the input element

  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState('');
  const [imagePreview, setImagePreview] = useState('');

  const handleFileChange = (event) => {
    const selectedImage = event.target.files[0];

    if (selectedImage) {
      setImage(selectedImage);

      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(selectedImage);
    }
  };

  const handleSubmit = async () => {
    if (!image) {
      alert('Please select an image');
      return;
    }

    const formData = new FormData();
    formData.append('image', image);

    try {
      const response = await fetch(api_base_url, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setPrediction(data.prediction);
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleClearImage = () => {
    setImage(null);
    setImagePreview('');
    setPrediction('');
    if (fileInputRef.current) {
      fileInputRef.current.value = ''; // Reset input value to clear the selected file
    }
  };

  return (
    <div className='home-container'>
      <h1>Skin Disease Prediction from Image </h1>
      <input type="file" onChange={handleFileChange} ref={fileInputRef}/>
      {imagePreview && <img src={imagePreview} alt="Selected" style={{ maxWidth: '100%' }} />}
      <button className='predict-btn' onClick={handleSubmit}>Predict</button>
      {prediction && <p className='prediction-text'>Prediction: {prediction}</p>}
      {imagePreview && <button onClick={handleClearImage}>Clear Image</button>}
    </div>
  )
}

export default Home