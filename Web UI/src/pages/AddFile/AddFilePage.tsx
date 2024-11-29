import { useState } from 'react';
import FileInputField from './FileInputField';
import SeparateTracksCheckbox from './SeparateTracksCheckbox';
import { Link } from 'react-router';

const AddFile = () => {
  const [file, setFile] = useState<File>();
  const [separateTracks, setSeparateTracks] = useState<boolean>(false);

  console.log(file, separateTracks);

  return (
    <main id='add_file_page'>
      <FileInputField setFile={setFile} />
      <SeparateTracksCheckbox setSeparateTracks={setSeparateTracks} />
      <button disabled={!file} id="upload_button">Next</button>
      <Link to="about">?</Link>
    </main>
  );
};

export default AddFile;
