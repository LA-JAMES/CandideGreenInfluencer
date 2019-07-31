import React from 'react';
import './App.css';

import ShowImageTile from './components/image_tile'
import ShowImageAnalysis from './components/featured_image_analysis'

import logo from './images/candide-logo.png'

function App() {

  let no_img = "I haven't been able to match any images."

  return (
    <div className="App">
    <br/>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />

        <span>
            <h1>WELCOME TO GREEN INFLUENCER!</h1>
            <h2>Your Image...</h2>
        </span>

        <ShowImageTile file={window.submission} type='Submission' categories={window.submission_categories} tile='submitted' />

        <h2>Other posts like yours...</h2>
        {window.similar_images.length > 0 ? <ShowImageTile file={window.similar_images[0]} type='Rank 1.' categories={window.similar_categories[0]} tile='similar'/> : null }
        {window.similar_images.length > 1 ? <ShowImageTile file={window.similar_images[1]} type='Rank 2.' categories={window.similar_categories[1]} tile='similar'/> : null }
        {window.similar_images.length > 2 ? <ShowImageTile file={window.similar_images[2]} type='Rank 3.' categories={window.similar_categories[2]} tile='similar'/> : null }
        {window.similar_images.length > 3 ? <ShowImageTile file={window.similar_images[3]} type='Rank 4.' categories={window.similar_categories[3]} tile='similar'/> : null }
        {window.similar_images.length > 4 ? <ShowImageTile file={window.similar_images[4]} type='Rank 5.' categories={window.similar_categories[4]} tile='similar'/> : null }
        {window.similar_images.length === 0 ? <p>{no_img}</p> : null }

        <h2>Featured Image...</h2>
        <ShowImageTile file={window.proc_img} type='Featured Image (OpenCV): ' features={window.proc_img_features} analysis={window.proc_analysis} tile='featured'/>
        <ShowImageAnalysis/>
        <br/>

      </header>
    </div>
  );
}

export default App;
