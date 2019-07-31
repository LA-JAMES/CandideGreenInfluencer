import React from 'react';

import img1 from '../images/1.jpg'
import img2 from '../images/2.jpg'
import img3 from '../images/3.jpg'
import img4 from '../images/4.jpg'
import img5 from '../images/5.jpg'
import img6 from '../images/6.jpg'
import img7 from '../images/7.jpg'
import img8 from '../images/8.jpg'
import img9 from '../images/9.jpg'
import img10 from '../images/10.jpg'
import img11 from '../images/11.jpg'
import img12 from '../images/12.jpg'
import img13 from '../images/13.jpg'
import img14 from '../images/14.jpg'
import img15 from '../images/15.jpg'
import img16 from '../images/16.jpg'
import img17 from '../images/17.jpg'
import img18 from '../images/18.jpg'
import img19 from '../images/19.jpg'
import img20 from '../images/20.jpg'


function ShowImageTile(props){

    let categories_string = ''
    let subtitle_text = ''

    if (Array.isArray(props.categories)) {
        categories_string = props.categories.join(', ')
    }

    if (props.tile === 'similar'){
        subtitle_text = 'Matched on Categories:'
    } else if (props.tile === 'submitted'){
        subtitle_text = 'Categories Found:'
    } else if (props.tile === 'featured'){
        subtitle_text = `${props.features} similar features!`
    }

    return(

    <div id="similar_image_tile">
        <div id="tile-text">
            <p>{props.type}</p>
            <h2>{props.file}</h2>
            <h3>{subtitle_text}</h3>
            <p>{categories_string}</p>
        </div>
        <span>
            <img src={props.file === '1.jpg'? img1 : null} alt=''/>
            <img src={props.file === '2.jpg'? img2 : null} alt=''/>
            <img src={props.file === '3.jpg'? img3 : null} alt=''/>
            <img src={props.file === '4.jpg'? img4 : null} alt=''/>
            <img src={props.file === '5.jpg'? img5 : null} alt=''/>
            <img src={props.file === '6.jpg'? img6 : null} alt=''/>
            <img src={props.file === '7.jpg'? img7 : null} alt=''/>
            <img src={props.file === '8.jpg'? img8 : null} alt=''/>
            <img src={props.file === '9.jpg'? img9 : null} alt=''/>
            <img src={props.file === '10.jpg'? img10 : null} alt=''/>
            <img src={props.file === '11.jpg'? img11 : null} alt=''/>
            <img src={props.file === '12.jpg'? img12 : null} alt=''/>
            <img src={props.file === '13.jpg'? img13 : null} alt=''/>
            <img src={props.file === '14.jpg'? img14 : null} alt=''/>
            <img src={props.file === '15.jpg'? img15 : null} alt=''/>
            <img src={props.file === '16.jpg'? img16 : null} alt=''/>
            <img src={props.file === '17.jpg'? img17 : null} alt=''/>
            <img src={props.file === '18.jpg'? img18 : null} alt=''/>
            <img src={props.file === '19.jpg'? img19 : null} alt=''/>
            <img src={props.file === '20.jpg'? img20 : null} alt=''/>
        </span>
    </div>

    )
}

export default ShowImageTile;


