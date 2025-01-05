import { useState } from 'react';
import { IAnalyzeType } from '../store/pipelineApi';

export interface IPipelineStep {
  startTime: number;
  endTime: number;
  track: string;
  type: string;
  id: number;
  analyzeType?: IAnalyzeType;
  setAnalyzeType: (_: IAnalyzeType) => void;
  removeSelf: () => void;
}

const usePipeline = () => {
  const handleAddStep = () => {
    setPipeline((prev) => {
      const newStep = { ...defaultStep };
      newStep.id = Date.now();
      newStep.removeSelf = handleRemoveStep(newStep.id);
      newStep.setAnalyzeType = handleSelectAnalyzeType(newStep.id);
      return [...prev, newStep];
    });
  };

  const handleRemoveStep = (id: number) => () => {
    setPipeline((prev) => prev.filter((pipeline) => pipeline.id !== id));
  };

  const handleSelectAnalyzeType = (id: number) => (type: IAnalyzeType) => {
    setPipeline((prev) =>
      prev.map((step) => {
        if (step.id === id) step.analyzeType = type;
        return step;
      })
    );
  };

  const defaultStep: IPipelineStep = {
    startTime: 0,
    endTime: 0,
    track: '',
    type: '',
    id: 0,
    removeSelf: handleRemoveStep(0),
    setAnalyzeType: handleSelectAnalyzeType(0)
  };

  const [pipeline, setPipeline] = useState<IPipelineStep[]>([defaultStep]);

  return { pipeline, handleAddStep };
};

export default usePipeline;
