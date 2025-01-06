import { IPipelineStep } from '../../../hooks/usePipeline';
import PipelineStepInput from './PipelineStepInput';

interface Props {
  step: IPipelineStep;
}

const PipelineStepBody = ({ step }: Props) => {
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
