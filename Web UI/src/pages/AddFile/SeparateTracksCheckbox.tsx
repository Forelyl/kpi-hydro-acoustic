import { ChangeEvent, Dispatch, SetStateAction } from 'react';

interface Props {
  setSeparateTracks: Dispatch<SetStateAction<boolean>>;
}

const SeparateTracksCheckbox = ({ setSeparateTracks }: Props) => {
  const handleCheck = (e: ChangeEvent<HTMLInputElement>) => {
    setSeparateTracks(e.target.checked);
  };

  return (
    <div id="separate_tracks">
      <label htmlFor='separate'>Separate multiple tracks</label>
      <input type="checkbox" id="separate" onChange={handleCheck} />
      <label htmlFor="separate" className="custom_checkbox"></label>
    </div>
  );
};

export default SeparateTracksCheckbox;
