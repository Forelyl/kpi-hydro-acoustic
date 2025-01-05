import { IPipelineStep } from '../../../hooks/usePipeline';
import TimeBounds from '../TimeBounds/TimeBounds';
import PipelineStepHeader from './PipelineStepHeader';

interface Props {
  step: IPipelineStep;
}

const PipelineStep = ({ step }: Props) => {
  return (
    <div className="pipline_step">
      <PipelineStepHeader step={step} />
      <TimeBounds />
    </div>
  );
};

export default PipelineStep;
