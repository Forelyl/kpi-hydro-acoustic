import SelectOpenIcon from '../../components/icons/SelectOpenIcon';
import { useGetAnalizeTypesQuery } from '../../store/pipelineApi';

const AnalyzeTypeSelect = () => {
  const { data: analizeTypes, isLoading, error } = useGetAnalizeTypesQuery();

  if (error) console.log(error);
  console.log(analizeTypes);

  return (
    <div className="select_container type_select">
      <select defaultValue="Analyze type" className="select ">
        <option hidden>Analyze type</option>

        {!isLoading &&
          analizeTypes?.length &&
          analizeTypes.map((type, index) => (
            <option key={index} value={index}></option>
          ))}
      </select>
      <div className="image_container">
        <SelectOpenIcon />
      </div>
    </div>
  );
};

export default AnalyzeTypeSelect;
