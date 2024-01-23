import axios from 'axios'
import {Button ,RadioButton,Input} from "@react95/core"
import React, { useState,useRef } from "react"

export function UploadModel() {
    const [selectedOptionModel, onChangeModel] = React.useState(null);
    const handleChangeModel = (e) => {
      onChangeModel(e.target.value);
    };
  
    //input name model
    const [inputValue, setInputValue] = useState('');
    const handleInputChange = (e) => {
      setInputValue(e.target.value);
    };
  
    const [selectedFilepth, setSelectedFilepth] = useState(null);
    const handleFileChangepth = (e) => {
      const file = e.target.files[0]; // Get the first selected file
      if (file && file.size > 500 * 1024 * 1024) {
        alert('File size pth model exceeds the maximum limit of 500MB.');
        // You may want to clear the file input value here
        e.target.value = null;
      }else if (file && file.size <= 500 * 1024 * 1024 && file.name.endsWith('.pth')){
        setSelectedFilepth(file)
        //console.log('pth pass')
      }else{
        e.target.value = null;
        alert('Error');
      }
      
    };
  
    const [selectedFileindex, setSelectedFileindex] = useState(null);
    const handleFileChangeindex = (e) => {
      const file = e.target.files[0]; // Get the first selected file
      if (file && file.size > 500 * 1024 * 1024) {
        alert('File size index model exceeds the maximum limit of 500MB.');
        // You may want to clear the file input value here
        e.target.value = null;
      }else if (file && file.size <= 500 * 1024 * 1024 && file.name.endsWith('.index') ){
        setSelectedFileindex(file)
        //console.log('index pass')
      }else{
        e.target.value = null;
        alert('Error');
      }
    };
  
  
    
    const handleClickupload = () => {
      if (selectedOptionModel == null){
        //console.log('null!') 
        alert('Please input model name');
      }else if (selectedOptionModel == 'have_index' &&	inputValue != ''){
        console.log('have index!')
        console.log(inputValue)
        console.log('Selected File:', selectedFilepth);
        console.log(selectedFileindex)
  
      }else if (selectedOptionModel == 'no_index' &&	inputValue != ''){
        console.log('not have index!')
        console.log(inputValue)
        onfilesubmitRef.current.value = null;
        console.log('Selected File:', selectedFilepth);
      }else {
        // alert error
        alert('Error');
        //console.log('error')
      }
    };
  
    return (
      <>
        <h3>Upload model</h3>
        <p>Modelname</p>
        <Input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Type model name"
        />
        <br/>
        <br/>
        <RadioButton
          name="have_index"
          value="have_index"
          checked={selectedOptionModel === 'have_index'}
          onChange={handleChangeModel}
        >
          have index file
        </RadioButton>
        <RadioButton
          name="no_index"
          value="no_index"
          checked={selectedOptionModel === 'no_index'}
          onChange={handleChangeModel}
        >
          not have index file
        </RadioButton>
        <p>pth file</p>
        <input 
        type="file" 
        id="mypthFile" 
        name="pth_filename" 
        accept=".pth"
        multiple={false}
        onChange={handleFileChangepth }
        />
  
        {selectedOptionModel === 'have_index' && (
          <>
            <p>index file</p>
            <input 
            type="file" 
            id="myIndexFile" 
            name="index_filename" 
            accept=".index"
            multiple={false}
           
            onChange={handleFileChangeindex }
            />
          </>
        )}
        <Button onClick={handleClickupload}>Upload</Button>
      </>
    );
}

export default UploadModel