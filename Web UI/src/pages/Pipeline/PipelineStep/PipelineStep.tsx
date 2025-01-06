import { useState } from 'react';
import { IPipelineStep } from '../../../hooks/usePipeline';
import PipelineStepBody from './PipelineStepBody';
import PipelineStepHeader from './PipelineStepHeader';

interface Props {
  step: IPipelineStep;
}

const PipelineStep = ({ step }: Props) => {
  const [empyState, setEmptyState] = useState(true);


  return (
    <div className="pipline_step">
      <PipelineStepHeader step={step} emptyState={empyState}/>
      <PipelineStepBody step={step} setEmptyState={setEmptyState}/>
    </div>
  );
};

export default PipelineStep;
