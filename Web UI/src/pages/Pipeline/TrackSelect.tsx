import SelectOpenIcon from '../../components/icons/SelectOpenIcon';
import { useAppSelector } from '../../store/store';

const TrackSelect = () => {
  const { channels } = useAppSelector((state) => state.loadedFile);

  return (
    <div className="select_container track_select">
      <select defaultValue="Track select" className="select">
        <option hidden>Track select</option>
        {Array.from({ length: channels }).map((_, i) => (
          <option key={i + 1} value={i + 1}>
            {i + 1}
          </option>
        ))}
      </select>
      <div className="image_container">
        <SelectOpenIcon />
      </div>
    </div>
  );
};

export default TrackSelect;
