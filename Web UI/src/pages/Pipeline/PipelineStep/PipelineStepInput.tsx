import { ChangeEvent } from 'react';
import { IAnalyzeTypeArg } from '../../../store/pipelineApi';
import TimeInput from '../TimeInput';
import { IPipelineStep } from '../../../hooks/usePipeline';

interface Props {
  arg: IAnalyzeTypeArg;
  step: IPipelineStep;
  index: number;
}

const renderInputField = (
  datatype: string,
  setData: (_: number | Record<string, number>) => void
) => {
  const handlePositiveFloat = (e: ChangeEvent<HTMLInputElement>) => {
    setData(+e.target.value);
  };

  const handleFloat = (e: ChangeEvent<HTMLInputElement>) => {
    setData(+e.target.value);
  };

  const handleNonNegativeFloat = (e: ChangeEvent<HTMLInputElement>) => {
    setData(+e.target.value);
  };

  switch (datatype) {
    case 'Time':
      return <TimeInput onChange={setData} />;
    case 'Positive float':
      return (
        <input onChange={handlePositiveFloat} min={0} type="number" required />
      );
    case 'Float':
      return <input onChange={handleFloat} type="number" required />;
    case 'Non negative float':
      return (
        <input
          onChange={handleNonNegativeFloat}
          min={0}
          type="number"
          required
        />
      );
    default:
      return <div>Not implemented</div>;
  }
};

const PipelineStepInput = ({ arg, index, step }: Props) => {
  const handleSetData =
    (index: number) => (data: number | Record<string, number>) => {
      const newData = [...(step.data ?? [])];
      newData[index] = data;
      step.setData(newData);
    };

  return (
    <div className="time_select">
      <div className="label_box">
        <label htmlFor="start-time" title={arg.description}>
          {arg.name}
          {arg.units ? `, ${arg.units}` : ''}
        </label>
        {renderInputField(arg.datatype, handleSetData(index))}
      </div>
    </div>
  );
};

export default PipelineStepInput;
