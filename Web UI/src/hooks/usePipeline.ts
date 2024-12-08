import { useState } from 'react';

export interface IPipelineStep {
  startTime: number;
  endTime: number;
  track: string;
  type: string;
  id: number;
  removeSelf: () => void;
}

const usePipeline = () => {
  const handleAddStep = () => {
    setPipeline((prev) => {
      const newStep = { ...defaultStep };
      newStep.id = Date.now();
      newStep.removeSelf = handleRemoveStep(newStep.id);
      return [...prev, newStep];
    });
  };

  const handleRemoveStep = (id: number) => () => {
    setPipeline((prev) => prev.filter((pipeline) => pipeline.id !== id));
  };

  const defaultStep: IPipelineStep = {
    startTime: 0,
    endTime: 0,
    track: '',
    type: '',
    id: 0,
    removeSelf: handleRemoveStep(0)
  };

  const [pipeline, setPipeline] = useState<IPipelineStep[]>([defaultStep]);

  return { pipeline, handleAddStep };
};

export default usePipeline;
