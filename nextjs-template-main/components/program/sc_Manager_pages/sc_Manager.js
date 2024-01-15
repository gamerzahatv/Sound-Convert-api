import React, { useState,useRef } from "react";
import { List ,Checkbox ,Button ,RadioButton,Input, Modal} from "@react95/core";
import { Awfxcg321303 } from "@react95/icons";
import * as S from "../../layoutStyling";
import axios from 'axios';
import { UploadModel } from "./sc_upload_content";
import { Upload_music } from "./sc_upload_content";
import { Sound_view } from "./sc_crud_manage";
import { Apptest } from "./sc_crud_manage";




function SC_Manager({ closeSC_Manager, isMobile }) {
  return (
    <>
    
    <S.layoutMain
      // isMobile={isMobile}
      title={"SC_Manager.exe"}
      closeModal={closeSC_Manager}
      height="100%"
      icon={<Awfxcg321303 variant="32x32_4" />}
      menu={[
        {
          name: "Options",
          list: (
            <List>
              <List.Item onClick={closeSC_Manager}>Close</List.Item>
            </List>
          ),
        },
      ]}
    >
      <S.layoutMainContent bg="white" boxShadow="in">
        <S.textModal>
          <h1>SOUND CONVERT MANAGER</h1>
          <p>
            Bachelor studies in Audiovisual Media with a focus in user
            inter-action and multimedia studies. Thesis work on proactive UX
            design for a mobile interface. Exchange studies at Institut d'Études
            Politiques de Paris in Latin American Studies.
          </p>
          <h2>Mange </h2>
          <UploadModel/>           
          <Upload_music/>
          <Sound_view/>
        </S.textModal>
      </S.layoutMainContent>
    </S.layoutMain>
    </>
  );
}

export default SC_Manager;
