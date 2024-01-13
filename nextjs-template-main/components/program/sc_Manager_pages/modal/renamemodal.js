import { Modal, List, Frame, Button ,Input } from "@react95/core";
import React, { useState, useRef } from "react";
export function Renamemodal({value}) {
  const [showFirstModal, toggleShowFirstModal] = React.useState(false);
  const handleOpenFirstModal = () => toggleShowFirstModal(true)
  const handleCloseFirstModal = () => toggleShowFirstModal(false)


  const handleButtonClick_Accept = () => {
    alert(`Rename : ${value}`);
  }
  const handleButtonClick_Cancle = () => {
    handleCloseFirstModal();
  }
  return (
    <>
      <Button onClick={handleOpenFirstModal}>Rename</Button>
      {showFirstModal && (
        <Modal
          width="300"
          height="200"
          title={`Rename ${value} ?`}
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
                <p>test input</p>
                <Input/>
            </div>
           
        </Modal>
      )}
    </>
  );
}
