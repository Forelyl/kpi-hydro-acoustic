import { ChangeEvent } from 'react';
import SelectOpenIcon from '../../components/icons/SelectOpenIcon';
import { useGetAnalizeTypesQuery } from '../../store/pipelineApi';
import { IPipelineStep } from '../../hooks/usePipeline';

interface Props {
  step: IPipelineStep;
}

const AnalyzeTypeSelect = ({ step }: Props) => {
  const { data: analizeTypes, isLoading } = useGetAnalizeTypesQuery();

  const handleSelectAnalyzeType = (e: ChangeEvent<HTMLSelectElement>) => {
    if (analizeTypes && !isLoading) {
      step.setData([]);
      step.setAnalyzeType(
        analizeTypes.find((type) => type.name === e.target.value)!
      );
    }
  };

  return (
    <div className="select_container type_select">
      <select
        onChange={handleSelectAnalyzeType}
        defaultValue="Analyze type"
        className="select ">
        <option hidden>Analyze type</option>

        {!isLoading &&
          analizeTypes?.length &&
          analizeTypes.map((type) => (
            <option key={type.f_id} value={type.name}>
              {type.name}
            </option>
          ))}
      </select>
      <div className="image_container">
        <SelectOpenIcon />
      </div>
    </div>
  );
};

export default AnalyzeTypeSelect;
