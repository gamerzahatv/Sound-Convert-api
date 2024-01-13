import React, { useState, useRef } from "react";
import {
  List,
  Fieldset,
  Dropdown,
  Button,
  Input,
  RadioButton,
  Range,
} from "@react95/core";
import { Awfxcg321303 } from "@react95/icons";
import * as S from "../layoutStyling";
import { marginTop } from "@xstyled/styled-components";

function Yourmodel() {
  const [selectedOptionownmodel, setSelectedOptionownmodel] = React.useState(
    []
  );
  const handleChangeOptionownmodel = (e) => {
    setSelectedOptionownmodel(e.target.value);
    console.log(e.target.value);
  };
  const handleRefreshownmodel = () => {
    // Add the logic for refreshing here
    console.log("Refresh button clicked ownmodel");
    console.log("Selected Option:", selectedOptionownmodel);
  };
  const options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"];
  return (
    <>
      <p>
        You choose your own model. Click the refresh button to load the
        available models, then use the dropdown to select the model you want.
      </p>
      <div style={{ display: "flex", alignItems: "flex-start" }}>
        <Fieldset legend="Choose your own model" className="contentmodelfield">
          <Dropdown options={options} onChange={handleChangeOptionownmodel} />
          <Button
            className="buttonmodelcontentfield"
            onClick={handleRefreshownmodel}
          >
            Refresh
          </Button>
        </Fieldset>
      </div>
      <p>You Select : {selectedOptionownmodel}</p>
    </>
  );
}

function Minemodel() {
  const [selectedOptionmodelprovide, setSelectedOptionmodelprovide] =
    React.useState([]);
  const handleChangeOptionmodelprovide = (e) => {
    setSelectedOptionmodelprovide(e.target.value);
    console.log(e.target.value);
  };
  const options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"];
  const handleRefreshmodelprovide = () => {
    // Add the logic for refreshing here
    console.log("Refresh button clicked modelprovide");
    console.log("Selected Option:", selectedOptionmodelprovide);
  };

  //slider  volume_envelope_scaling
  const sliderReffeature_ratio = useRef(null);
  const [
    sliderValuefeature_ratio,
    setSliderValuefeature_ratio,
  ] = useState(0);
  const handleSliderChangefeature_ratio = () => {
    // Access the current value of the slider using the ref
    const valuefeature_ratio =
      sliderReffeature_ratio.current.value;

    // Update the state with the new value
    setSliderValuefeature_ratio(valuefeature_ratio);
    console.log(valuefeature_ratio);
  };

  const handleInputChangefeature_ratio = (event) => {
    const valuefeature_ratio = event.target.value;
    setSliderValuefeature_ratio(valuefeature_ratio);
  };
  
  return (
    <>
      <p>
        You choose model provide. Click the refresh button to load the available
        models, then use the dropdown to select the model you want.
      </p>
      <div style={{ display: "flex", alignItems: "flex-start" }}>
        <Fieldset legend="Choose a model provide" className="contentmodelfield">
          <Dropdown
            options={options}
            onChange={handleChangeOptionmodelprovide}
          />
          <Button
            className="buttonmodelcontentfield"
            onClick={handleRefreshmodelprovide}
          >
            Refresh
          </Button>
        </Fieldset>
      </div>
      <p>You Select : {selectedOptionmodelprovide}</p>      
      <p>Search feature ratio controls accent strength, too high has artifacting </p>
      <p>
        After you click Refresh, the index path will be automatically detected.
      </p>
      <Fieldset
        legend="Search feature ratio"
        className="contentmodelfield"
      >
        <Range 
          step="0.01"
          min="0"
          max="1"
          value={sliderValuefeature_ratio}
          onChange={handleSliderChangefeature_ratio}
          ref={sliderReffeature_ratio}
        />
        <Input className="generalrangecontent" 
          value={sliderValuefeature_ratio}
          onChange={handleInputChangefeature_ratio}
        />
      </Fieldset>
      <p>Index feature ratio  is :{sliderValuefeature_ratio}</p>
    </>
  );
}

function SC_Process({ closeSC_Process }) {
  //select minemodel or yourmodel
  const [selectedOptionmodel, setSelectedOption] = React.useState(null);
  const handleChangeOptionmodel = (e) => {
    setSelectedOption(e.target.value);
    //console.log(e.target.value)
  };

  // The component to be shown when the radio button is clicked
  const RenderComponent = () => {
    //one is minemodel
    if (selectedOptionmodel === "one") {
      return <Minemodel />;
    } else if (selectedOptionmodel === "two") {
      return <Yourmodel />;
    } else {
      // Handle other cases if necessary
      return null;
    }
  };

  // select pitchalgorithm
  const [selectedOptionpitchalgorithm, setSelectedOptionpitchalgorithm] =
    React.useState(null);
  const handleChangeOptionpitchalgorithm = (e) => {
    setSelectedOptionpitchalgorithm(e.target.value);
    console.log(e.target.value);
  };

  //slider   median filtering
  const sliderRefmedianfiltering = useRef(null);
  const [sliderValuemedianfiltering, setSliderValuemedianfiltering] = useState(0);
  const handleSliderChangemedianfiltering = () => {
    // Access the current value of the slider using the ref
    const valuemedianfiltering = sliderRefmedianfiltering.current.value;

    // Update the state with the new value
    setSliderValuemedianfiltering(valuemedianfiltering);
    console.log(valuemedianfiltering);
  };

  const handleInputChangemedianfiltering = (event) => {
    const value = event.target.value;
    setSliderValuemedianfiltering(value);
  };

  //slider  volume_envelope_scaling
  const sliderRefvolume_envelope_scaling = useRef(null);
  const [
    sliderValuevolume_envelope_scaling,
    setSliderValuevolume_envelope_scaling,
  ] = useState(0);
  const handleSliderChangevolume_envelope_scaling = () => {
    // Access the current value of the slider using the ref
    const valuevolume_envelope_scaling =
      sliderRefvolume_envelope_scaling.current.value;

    // Update the state with the new value
    setSliderValuevolume_envelope_scaling(valuevolume_envelope_scaling);
    console.log(valuevolume_envelope_scaling);
  };

  const handleInputChangevolume_envelope_scaling = (event) => {
    const valuevolume_envelope_scaling = event.target.value;
    setSliderValuevolume_envelope_scaling(valuevolume_envelope_scaling);
  };

  //slider  protect voice
  const sliderRefprotect_voice = useRef(null);
  const [
    sliderValueprotect_voice,
    setSliderValueprotect_voice,
  ] = useState(0);
  const handleSliderChangeprotect_voice = () => {
    // Access the current value of the slider using the ref
    const valueprotect_voice =
      sliderRefprotect_voice.current.value;

    // Update the state with the new value
    setSliderValueprotect_voice(valueprotect_voice);
    console.log(valueprotect_voice);
  };

  const handleInputChangeprotect_voice = (event) => {
    const valueprotect_voice = event.target.value;
    setSliderValueprotect_voice(valueprotect_voice);
  };

  // handle convert button
  const handleconvert = () => {
    // Add the logic for refreshing here
    console.log("Convert");
    console.log(
      "Selected pitch extraction algorithm:",
      selectedOptionpitchalgorithm
    );
  };
  return (
    <>
      <S.layoutMain
        // isMobile={isMobile}
        title={"SC_Process.exe"}
        closeModal={closeSC_Process}
        height="100%"
        icon={<Awfxcg321303 variant="32x32_4" />}
        menu={[
          {
            name: "Options",
            list: (
              <List>
                <List.Item onClick={closeSC_Process}>Close</List.Item>
              </List>
            ),
          },
        ]}
      >
        <S.layoutMainContent bg="white" boxShadow="in">
          <S.textModal>
            <h1>SOUND CONVERT_model</h1>
            <p>Convert Sound</p>
            <h2>Step 1 Choose a model </h2>
            <p>
              Choose whether you will use the model yours or the model we
              provide
            </p>

            <Fieldset legend="Choose a Options">
              <RadioButton
                name="working"
                value="one"
                checked={selectedOptionmodel === "one"}
                onChange={handleChangeOptionmodel}
              >
                Use the model provided
              </RadioButton>
              <RadioButton
                name="working"
                value="two"
                checked={selectedOptionmodel === "two"}
                onChange={handleChangeOptionmodel}
              >
                Use your own model
              </RadioButton>
            </Fieldset>

            <RenderComponent />

            <h2>Step 2 Choose a sound </h2>
            <p>
              It is recommended that the audio file extension be .wav or .mp3
            </p>
            <div style={{ display: "flex", alignItems: "flex-start" }}>
              <Fieldset legend="Choose a sound" className="contentmodelfield">
                <Dropdown />
                <Button className="buttonmodelcontentfield">Refresh</Button>
              </Fieldset>
            </div>

            <h2>Step 3 Change pitch (Options) </h2>
            <p>
              Transpose integer, number of semitones, raise by an octave: 12,
              lower by an octave: -12
            </p>
            <Input />

            <h2>Step 4 Select the pitch extraction algorithm </h2>
            <p>
              Select the pitch extraction algorithm ('pm': faster extraction but
              lower-quality speech; 'harvest': better bass but extremely slow;
              'crepe': better quality but GPU intensive), 'rmvpe': best quality,
              and little GPU requirement
            </p>

            <Fieldset legend="Select the pitch extraction algorithm">
              <RadioButton
                name="working"
                value="pm"
                checked={selectedOptionpitchalgorithm === "pm"}
                onChange={handleChangeOptionpitchalgorithm}
              >
                pm
              </RadioButton>
              <RadioButton
                name="working"
                value="havest"
                checked={selectedOptionpitchalgorithm === "havest"}
                onChange={handleChangeOptionpitchalgorithm}
              >
                havest
              </RadioButton>
              <RadioButton
                name="working"
                value="crepe"
                checked={selectedOptionpitchalgorithm === "crepe"}
                onChange={handleChangeOptionpitchalgorithm}
              >
                crepe
              </RadioButton>
              <RadioButton
                name="working"
                value="rmpve"
                checked={selectedOptionpitchalgorithm === "rmpve"}
                onChange={handleChangeOptionpitchalgorithm}
              >
                rmvpe
              </RadioButton>
            </Fieldset>
            <br></br>
            <h2>Step 5 median filtering (Options) </h2>
            <p>
              If greater than or equal to 3 : apply median filtering to the
              harvested pitch results. The value represents the filter radius
              and can reduce breathiness. (0-7)
            </p>
            <Fieldset
              legend="Customize median filtering"
              className="contentmodelfield"
            >
              <Range
                min="0"
                max="7"
                value={sliderValuemedianfiltering}
                onChange={handleSliderChangemedianfiltering}
                ref={sliderRefmedianfiltering}
              />
              <Input
                className="generalrangecontent"
                value={sliderValuemedianfiltering}
                onChange={handleInputChangemedianfiltering}
              />
            </Fieldset>
            <p>median filtering Value: {sliderValuemedianfiltering}</p>

            <h2>Step 6 Adjust the volume envelope scaling (Options) </h2>
            <p>
              Adjust the volume envelope scaling. Closer to 0, the more it
              mimicks the volume of the original vocals. Can help mask noise and
              make volume sound more natural when set relatively low. Closer to
              1 will be more of a consistently loud volume:
            </p>
            <Fieldset
              legend="Adjust the volume envelope scaling"
              className="contentmodelfield"
            >
              <Range
                min="0"
                max="1"
                step="0.01"
                value={sliderValuevolume_envelope_scaling}
                onChange={handleSliderChangevolume_envelope_scaling}
                ref={sliderRefvolume_envelope_scaling}
              />
              <Input
                className="generalrangecontent"
                value={sliderValuevolume_envelope_scaling}
                onChange={handleInputChangevolume_envelope_scaling}
              />
            </Fieldset>
            <p>
              Adjust the volume envelope scaling Value: {sliderValuevolume_envelope_scaling}
            </p>

            <h2>
              Step 7 Protect voiceless consonants and breath sounds (Options)
            </h2>
            <p>
              Protect voiceless consonants and breath sounds to prevent
              artifacts such as tearing in electronic music. Set to 0.5 to
              disable. Decrease the value to increase protection, but it may
              reduce indexing accuracy:
            </p>
            <Fieldset
              legend="Protect voiceless consonants and breath sounds"
              className="contentmodelfield"
            >
              <Range 
                min="0"
                max="0.5"
                step="0.01"
                value={sliderValueprotect_voice}
                onChange={handleSliderChangeprotect_voice}
                ref={sliderRefprotect_voice}
              />
              <Input  
                className="generalrangecontent"
                value={sliderValueprotect_voice}
                onChange={handleInputChangeprotect_voice}
              />
            </Fieldset>
            <p>protect voice is : {sliderValueprotect_voice}</p>

            <Button onClick={handleconvert}>Convert</Button>
          </S.textModal>
        </S.layoutMainContent>
      </S.layoutMain>
    </>
  );
}

export default SC_Process;
