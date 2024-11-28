import { ChangeEvent, Dispatch, SetStateAction } from 'react';

interface Props {
  setSeparateTracks: Dispatch<SetStateAction<boolean>>;
}

const SeparateTracksCheckbox = ({ setSeparateTracks }: Props) => {
  const handleCheck = (e: ChangeEvent<HTMLInputElement>) => {
    setSeparateTracks(e.target.checked);
  };

  return (
    <div>
      <span>Separate multiple tracks</span>
      <input type="checkbox" onChange={handleCheck} />
    </div>
  );
};

export default SeparateTracksCheckbox;
