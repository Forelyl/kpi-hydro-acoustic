import { ChangeEvent, Dispatch, SetStateAction, useRef, useState } from 'react';
import FileInputIcon from '../../components/icons/FileInputIcon';

interface Props {
  setFile: Dispatch<SetStateAction<File | undefined>>;
}

const FileInputField = ({ setFile }: Props) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [inputText, setInputText] = useState<string>("Add file");

  const handleSelectFile = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.item(0);
    if (file) {
      setFile(file);
      setInputText(file.name);
    } 
  };
  

  return (
    <div id='file_input' onClick={handleSelectFile}>
      <div></div>
      <span>{inputText}</span>
      <input
        type="file"
        accept="audio/wav"
        style={{ display: 'none' }}
        ref={fileInputRef}
        onChange={handleFileChange}
      />
      <FileInputIcon />
    </div>
  );
};

export default FileInputField;
