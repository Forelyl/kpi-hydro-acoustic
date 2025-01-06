import FileInputField from './FileInputField';
import SeparateTracksCheckbox from './SeparateTracksCheckbox';
import { Link, useNavigate } from 'react-router';
import { useAppDispatch, useAppSelector } from '../../store/store';
import Modal from '../../components/Modal/Modal';
import { resetError } from '../../store/loadedFileSlice';

const AddFile = () => {
  const dispatch = useAppDispatch();
  const { file, error } = useAppSelector((state) => state.loadedFile);
  const navigate = useNavigate();

  const handleNext = () => {
    void navigate('/pipeline');
  };

  return (
    <main id="add_file_page">
      <FileInputField />
      <SeparateTracksCheckbox />
      <button onClick={handleNext} disabled={!file} id="upload_button">
        Next
      </button>
      <Link to="about" draggable="false">?</Link>
      <Modal open={!!error}>
        <h2>{error?.title}</h2>
        <p>{error?.message}</p>
        <button onClick={() => dispatch(resetError())}>OK</button>
      </Modal>
    </main>
  );
};

export default AddFile;
