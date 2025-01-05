import { useState } from 'react';
import { IAnalyzeType } from '../store/pipelineApi';

export interface IPipelineStep {
  startTime: number;
  endTime: number;
  type: string;
  id: number;
  analyzeType?: IAnalyzeType;
  track?: number;
  setAnalyzeType: (_: IAnalyzeType) => void;
  setTrack: (_: number) => void;
  removeSelf: () => void;
}

const usePipeline = () => {
  const handleAddStep = () => {
    setPipeline((prev) => {
      const newStep = { ...defaultStep };
      newStep.id = Date.now();
      newStep.removeSelf = handleRemoveStep(newStep.id);
      newStep.setAnalyzeType = handleSelectAnalyzeType(newStep.id);
      newStep.setTrack = handleSelectTrack(newStep.id);
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

  const handleSelectTrack = (id: number) => (track: number) => {
    setPipeline((prev) =>
      prev.map((step) => {
        if (step.id === id) step.track = track;
        return step;
      })
    );
  };

  const defaultStep: IPipelineStep = {
    startTime: 0,
    endTime: 0,
    type: '',
    id: 0,
    removeSelf: handleRemoveStep(0),
    setAnalyzeType: handleSelectAnalyzeType(0),
    setTrack: handleSelectTrack(0)
  };

  const [pipeline, setPipeline] = useState<IPipelineStep[]>([defaultStep]);

  return { pipeline, handleAddStep };
};

export default usePipeline;
