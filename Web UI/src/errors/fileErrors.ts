type ErrorType = 'INVALID_FORMAT' | 'MANY_FILES';

export interface FileError {
  type: ErrorType;
  title: string;
  message: string;
}

export const fileErrors: Record<ErrorType, FileError> = {
  INVALID_FORMAT: {
    type: 'INVALID_FORMAT',
    title: 'Invalid file format',
    message: 'Please upload only wav or mp3'
  },
  MANY_FILES: {
    type: 'MANY_FILES',
    title: 'Too many files',
    message: 'You can only upload one file'
  }
};
