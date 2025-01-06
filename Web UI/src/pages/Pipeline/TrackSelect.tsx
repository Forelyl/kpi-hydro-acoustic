import { ChangeEvent } from 'react';
import SelectOpenIcon from '../../components/icons/SelectOpenIcon';
import { IPipelineStep } from '../../hooks/usePipeline';
import { useAppSelector } from '../../store/store';

interface Props {
  step: IPipelineStep;
}

const TrackSelect = ({ step }: Props) => {
  const { channels, separateTracks } = useAppSelector((state) => state.loadedFile);

  const handleSelectTrack = (e: ChangeEvent<HTMLSelectElement>) => {
    if (e.target.value) step.setTrack(+e.target.value);
  };

  return (
    <div className="select_container track_select">
      <select
        onChange={handleSelectTrack}
        defaultValue="Track select"
        className="select">
        <option hidden>Track select</option>
        { separateTracks ? (Array.from({ length: channels }).map((_, i) => (
          <option key={i + 1} value={i + 1}>
            {i + 1}
          </option>))) 
          : 
          (
            <option key='1' value='1'>
            1
            </option>
          )
        }
      </select>
      <div className="image_container">
        <SelectOpenIcon />
      </div>
    </div>
  );
};

export default TrackSelect;
