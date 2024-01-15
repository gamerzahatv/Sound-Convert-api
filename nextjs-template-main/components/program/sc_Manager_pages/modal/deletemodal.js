import { Modal, List,Button } from "@react95/core";
import React, { useEffect} from "react";
import axios from 'axios';
import { useRouter } from 'next/router';
import Swal from 'sweetalert2'

export function Deletemodal({value}) {
  //const router = useRouter();
  const [showFirstModal, toggleShowFirstModal] = React.useState(false);
  const handleOpenFirstModal = () => toggleShowFirstModal(true);
  const handleCloseFirstModal = () => toggleShowFirstModal(false);

  // const router = useRouter();
  const handleButtonClick_Accept = () => {
    
    const valuesArray = Object.values({value})
    const valuesString = valuesArray.toString();

    axios.delete(`http://localhost:5000/manage-sound/del?filename=${valuesString}`)
    .then(response => {
      //console.log(response);
      handleCloseFirstModal();
      //router.reload(); // Reload the page after deletion
      Swal.fire({
        title: 'Loading...',
        html: 'Please wait while we process your request.',
        showConfirmButton: false,
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        didOpen: () => {
          // This function will be called when the modal is opened
          // Use the mutate function to re-fetch and re-render data
          //router.push('/');
          
          setTimeout(() => {
            // Simulating an asynchronous task completion
            Swal.close(); // Close the loading popup after your task is done
            // Use mutate to re-fetch and re-render data
          }, 3000); // Adjust the timeout as needed
        },
      });
      

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
