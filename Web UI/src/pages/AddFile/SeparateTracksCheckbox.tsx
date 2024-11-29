import { ChangeEvent } from 'react';
import { useAppDispatch, useAppSelector } from '../../store/store';
import { setSeparateTracks } from '../../store/loadedFileSlice';

const SeparateTracksCheckbox = () => {
  const dispatch = useAppDispatch();
  const { separateTracks } = useAppSelector((state) => state.loadedFile);

  const handleCheck = (e: ChangeEvent<HTMLInputElement>) => {
    dispatch(setSeparateTracks(e.target.checked));
  };

  return (
    <div id="separate_tracks">
      <label htmlFor="separate">Separate multiple tracks</label>
      <input
        defaultChecked={separateTracks}
        type="checkbox"
        id="separate"
        onChange={handleCheck}
      />
      <label htmlFor="separate" className="custom_checkbox"></label>
    </div>
  );
};

export default SeparateTracksCheckbox;
