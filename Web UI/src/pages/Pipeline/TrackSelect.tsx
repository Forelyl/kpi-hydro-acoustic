import SelectOpenIcon from "../../components/icons/SelectOpenIcon";

const TrackSelect = () => {
  return (
    <div className="select_container track_select">
      <select defaultValue="Track select" className="select">
        <option hidden>Track select</option>
      </select>
      <div className="image_container">
        <SelectOpenIcon />
      </div>
    </div>
    
  );
};

export default TrackSelect;
