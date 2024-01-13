import { Modal, List, Frame, Button ,Input } from "@react95/core";
import React, { useState, useRef } from "react";
import axios from 'axios';
import { useRouter } from 'next/router';


export function Deletemodal({value}) {
  const router = useRouter();
  const [showFirstModal, toggleShowFirstModal] = React.useState(false);
  const handleOpenFirstModal = () => toggleShowFirstModal(true);
  const handleCloseFirstModal = () => toggleShowFirstModal(false);


  const handleButtonClick_Accept = () => {
    
    const valuesArray = Object.values({value})
    const valuesString = valuesArray.toString();

    axios.delete(`http://localhost:5000/del?filename=${valuesString}`)
    .then(response => {
      console.log(response);
      alert(`Rename : ${value}`);
      handleCloseFirstModal();
      //router.reload(); // Reload the page after deletion
    })
    .catch(error => {
      console.error(error);
     
    });
  }
  const handleButtonClick_Cancle = () => {
    handleCloseFirstModal();
  }





  return (
    <>
      <Button onClick={handleOpenFirstModal}>Delete</Button>
      {showFirstModal && (
        <Modal
          width="300"
          height="200"
          title={`Delete file ${value} ?`}
          defaultPosition={{
            x: 0,
            y: 20,
          }}
          closeModal={handleCloseFirstModal}
          buttons={[
            {
              value: "Ok",
              onClick: handleButtonClick_Accept,
            },
            {
              value: "Cancel",
              onClick: handleButtonClick_Cancle,
            },
          ]}
          menu={[
            {
              name: "File",
              list: (
                <List>
                  <List.Item onClick={handleCloseFirstModal}>Exit</List.Item>
                </List>
              ),
            },
          ]}
        >
            <div>
                <p>Delete this modal</p>
            </div>
           
        </Modal>
      )}
    </>
  );
}
