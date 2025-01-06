import { useEffect } from 'react';
import { IPipelineStep } from '../../../hooks/usePipeline';
import PipelineStepInput from './PipelineStepInput';

interface Props {
  step: IPipelineStep;
  setEmptyState: (isEmpty: boolean) => void;
}

const PipelineStepBody = ({ step, setEmptyState }: Props) => {

  useEffect(()=>{
    if (step.analyzeType?.args.length == 0) {
      setEmptyState(true)
    }
    else {
      setEmptyState(false)
    }
  }, [step, setEmptyState])

  return (
    <div className="fields_container">
      {step.analyzeType?.args.map((arg, index) => (
        <PipelineStepInput
          key={`${step.id}-${arg.name}`}
          step={step}
          arg={arg}
          index={index}
        />
      ))}
    </div>
  );
};

export default PipelineStepBody;
