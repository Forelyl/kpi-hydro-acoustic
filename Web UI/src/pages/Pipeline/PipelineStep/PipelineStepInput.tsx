import { ChangeEvent } from 'react';
import { IAnalyzeTypeArg } from '../../../store/pipelineApi';
import TimeInput from '../TimeInput';
import { IPipelineStep } from '../../../hooks/usePipeline';

interface Props {
  arg: IAnalyzeTypeArg;
  step: IPipelineStep;
  index: number;
}

const renderInputField = (datatype: string, setData: (_: number) => void) => {
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
      return <input onChange={handlePositiveFloat} type="number" required />;
    case 'Float':
      return <div className='time-input-wrapper'>
        <input className="time-input" onChange={handleFloat} type="number" required />
      </div>;
    case 'Non negative float':
      return <div className='time-input-wrapper'>
        <input className="time-input"
          onChange={handleNonNegativeFloat}
          min={0}
          type="number"
          required
        />
      </div>;
    default:
      return <div>Not implemented</div>;
  }
};

const PipelineStepInput = ({ arg, index, step }: Props) => {
  const handleSetData = (index: number) => (data: number) => {
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
