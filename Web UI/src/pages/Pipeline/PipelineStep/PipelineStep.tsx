import { IPipelineStep } from '../../../hooks/usePipeline';
import PipelineStepBody from './PipelineStepBody';
import PipelineStepHeader from './PipelineStepHeader';

interface Props {
  step: IPipelineStep;
}

const PipelineStep = ({ step }: Props) => {
  return (
    <div className="pipline_step">
      <PipelineStepHeader step={step} />
      <PipelineStepBody step={step} />
    </div>
  );
};

export default PipelineStep;
