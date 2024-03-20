import React, { useState } from 'react';
import axios from 'axios';
import './ImageResizer.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function ImageResizer() {
  const [image, setImage] = useState(null);
  const [width, setWidth] = useState('');
  const [height, setHeight] = useState('');
  const [resizedImage, setResizedImage] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [conversionType, setConversionType] = useState('');
  const [darkMode, setDarkMode] = useState(false); // State for dark mode

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
    setPreviewImage(URL.createObjectURL(e.target.files[0])); // Create a temporary URL for the uploaded image
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    setImage(droppedFile);
    setPreviewImage(URL.createObjectURL(droppedFile)); // Create a temporary URL for the dropped image
  };

  const handleConversionChange = (e) => {
    setConversionType(e.target.value);
  };

  const handleModeChange = () => {
    setDarkMode(!darkMode);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); 
    const formData = new FormData();
    formData.append('image', image);
    formData.append('width_px', width);
    formData.append('height_px', height);
    formData.append('format', conversionType);
    
    try {
      const response = await axios.post('https://image-resize-django.el.r.appspot.com/imageresizer/resizeimage/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      setResizedImage(response.data.data.link);
      setError(''); 
    } catch (error) {
      console.error('Error resizing image:', error);
      setError('An error occurred while resizing the image. Please try again.');
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div className={`container mt-5 ${darkMode ? 'dark-mode' : ''}`} style={darkMode ? { backgroundColor: '#333333', color: '#ffffff' } : null}>
  <div className="row justify-content-center">
    <div className="col-md-6">
      <h1 className="text-center mb-4">Image Resizer</h1>
      <form onSubmit={handleSubmit} onDrop={handleDrop} encType="multipart/form-data" className="dropzone">
        <div className="mb-3" style={darkMode ? { background: '#ffffff', color: '#a02398' } : null}>
          <input className="form-control" type="file" onChange={handleImageChange} />
          {previewImage && !loading && <img src={previewImage} alt="Uploaded" className="img-fluid mt-2" />} {/* Display image preview */}
          <p className="text-muted mt-2">- or -</p>
          <p className="text-muted mt-2">Drag & drop an image here</p>
        </div>
        <div className="mb-3">
          <div className="form-check">
            <input className="form-check-input" type="radio" id="pngRadio" name="conversionType" value="png" checked={conversionType === 'png'} onChange={handleConversionChange} />
            <label className="form-check-label" htmlFor="pngRadio">PNG</label>
          </div>
          <div className="form-check">
            <input className="form-check-input" type="radio" id="jpgRadio" name="conversionType" value="jpg" checked={conversionType === 'jpg'} onChange={handleConversionChange} />
            <label className="form-check-label" htmlFor="jpgRadio">JPG</label>
          </div>
          <div className="form-check">
            <input className="form-check-input" type="radio" id="webpRadio" name="conversionType" value="webp" checked={conversionType === 'webp'} onChange={handleConversionChange} />
            <label className="form-check-label" htmlFor="webpRadio">WebP</label>
          </div>
        </div>
        <div className="mb-3">
          <label htmlFor="widthInput" className="form-label">Width: {width}</label>
          <input type="range" className="form-range" id="widthInput" min="0" max="100" value={width} onChange={(e) => setWidth(e.target.value)} />
        </div>
        <div className="mb-3">
          <label htmlFor="heightInput" className="form-label">Height: {height}</label>
          <input type="range" className="form-range" id="heightInput" min="0" max="100" value={height} onChange={(e) => setHeight(e.target.value)} />
        </div>
        <button className="btn btn-primary" type="submit" disabled={loading}>
          {loading ? 'Resizing...' : 'Resize Image'}
        </button>
        <div className="form-check form-switch mt-3">
          <input className="form-check-input" type="checkbox" id="darkModeSwitch" checked={darkMode} onChange={handleModeChange} />
          <label className="form-check-label" htmlFor="darkModeSwitch">Dark Mode</label>
        </div>
      </form>
      {error && <p className="error-message mt-3">{error}</p>}
    </div>
  </div>
  {/* Bottom image tag for displaying result image */}
  {resizedImage && <img src={resizedImage} alt="Resized" className="img-fluid mt-3" />}
</div>
  );
}

export default ImageResizer;
