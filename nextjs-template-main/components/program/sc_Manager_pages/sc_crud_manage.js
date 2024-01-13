import useSWR from "swr";
import { useState } from "react";
import { Renamemodal } from "./modal/renamemodal";
import { Deletemodal } from "./modal/deletemodal";

export function Sound_view() {
  const [currentPage, setCurrentPage] = useState(1);
  const [pagecount, setpagecount] = useState(1);

  const { data, error } = useSWR(
    `http://localhost:5000/employees?start=${currentPage}&limit=5`,
    (url) => fetch(url).then((res) => res.json())
  );
  //const { data } = await res.json()
  //console.log(data)

  if (error) return <div>Failed to load</div>;
  if (!data) return <div>Loading...</div>;

  const handleButtonClick = (id) => {
    console.log(id)
  }

  const handleNextPage = () => {
    setCurrentPage((prevPage) => prevPage + 5);
    setpagecount(pagecount + 1);

  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prevPage) => prevPage - 5);
    }
    setpagecount(pagecount -1);

  };

  return (
    <>
      <div>
        <h1>Table CRUD SOUND</h1>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Text</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {data.results.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.text}</td>
                <td>
                  <Renamemodal value={item.text}/>
                  <Deletemodal value={item.text}/>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div>
          <button onClick={handlePreviousPage} disabled={currentPage === 1}>
            Previous
          </button>
          <span> page {pagecount} of {Math.ceil(data.count / 5)} </span>
          <button onClick={handleNextPage} disabled={pagecount * 5 >= data.count}>
            Next
          </button>
        </div>
      </div>
    </>
  );
};


