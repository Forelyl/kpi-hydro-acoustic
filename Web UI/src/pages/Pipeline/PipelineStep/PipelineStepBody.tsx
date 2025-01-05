import { IPipelineStep } from '../../../hooks/usePipeline';
import PipelineStepInput from './PipelineStepInput';

interface Props {
  step: IPipelineStep;
}

const PipelineStepBody = ({ step }: Props) => {
  return (
    <div className="fields_container">
      {step.analyzeType?.args.map((arg) => (
        <PipelineStepInput key={`${step.id}-${arg.name}`} arg={arg} />
      ))}
    </div>
  );
};

export default PipelineStepBody;
