type ErrorType = 'NO_TRACK_SELECTED';

export interface PipelineError {
  type: ErrorType;
  title: string;
  message: string;
}

export const pipelineErrors: Record<ErrorType, PipelineError> = {
  NO_TRACK_SELECTED: {
    type: 'NO_TRACK_SELECTED',
    title: 'Track is not selected',
    message: 'Please select track for all pipeline steps'
  }
};
