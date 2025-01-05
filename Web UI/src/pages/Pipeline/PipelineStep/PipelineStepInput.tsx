import { ChangeEvent, Dispatch, SetStateAction, useState } from 'react';
import { IAnalyzeTypeArg } from '../../../store/pipelineApi';
import TimeInput from '../TimeInput';

interface Props {
  arg: IAnalyzeTypeArg;
}

const renderInputField = (
  datatype: string,
  setData: Dispatch<SetStateAction<number>>
) => {
  const handlePositiveFloat = (e: ChangeEvent<HTMLInputElement>) => {
    e.target.value = e.target.value.replace(/[^0-9]/g, '');
    if (!+e.target.value) e.target.value = '';
    setData(+e.target.value);
  };

  const handleFloat = (e: ChangeEvent<HTMLInputElement>) => {
    setData(+e.target.value);
  };

  const handleNonNegativeFloat = (e: ChangeEvent<HTMLInputElement>) => {
    e.target.value = e.target.value.replace(/[^0-9]/g, '');
    setData(+e.target.value);
  };

  switch (datatype) {
    case 'Time':
      return <TimeInput onChange={setData} />;
    case 'Positive float':
      return <input onChange={handlePositiveFloat} type="number" required />;
    case 'Float':
      return <input onChange={handleFloat} type="number" required />;
    case 'Non negative float':
      return <input onChange={handleNonNegativeFloat} type="number" required />;
    default:
      return <div>Not implemented</div>;
  }
};

const PipelineStepInput = ({ arg }: Props) => {
  const [data, setData] = useState<number>(0);
  console.log(data);

  return (
    <div className="time_select">
      <div className="label_box">
        <label htmlFor="start-time" title={arg.description}>
          {arg.name}
          {arg.units ? `, ${arg.units}` : ''}
        </label>
        {renderInputField(arg.datatype, setData)}
      </div>
    </div>
  );
};

export default PipelineStepInput;
