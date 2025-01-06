import PipelineStep from './PipelineStep/PipelineStep';
import usePipeline from '../../hooks/usePipeline';
import PlusIcon from '../../components/icons/PlusIcon';
import SendIcon from '../../components/icons/SendIcon';
import { useSendPipelineMutation } from '../../store/pipelineApi';
import { useAppDispatch, useAppSelector } from '../../store/store';
import { useNavigate } from 'react-router';
import { setResultZip } from '../../store/loadedFileSlice';

const Pipeline = () => {
  const { pipeline, handleAddStep } = usePipeline();
  const [sendPipeline, {isLoading}] = useSendPipelineMutation();
  const { file, separateTracks } = useAppSelector((state) => state.loadedFile);
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const handleSendPipeline = () => {
    const steps = pipeline.map((step) => ({
      id: step.analyzeType?.id,
      track: [step.track],
      args: step.data
    }));

    const formData = new FormData();

    formData.append('file', file!);
    formData.append('separate', `${separateTracks}`);
    formData.append('pipeline', `{"pipeline": ${JSON.stringify(steps)}}`);

    sendPipeline(formData)
      .unwrap()
      .then((res) => {
        dispatch(setResultZip(res as Blob));
        void navigate('/download');
      })
      .catch(console.error);
  };
  return (
    <main id="pipline_page">
      {pipeline.map((step) => (
        <PipelineStep step={step} key={step.id} />
      ))}

      <div onClick={handleAddStep} className="add_step">
        <PlusIcon />
      </div>
      <div onClick={handleSendPipeline} className="add_step">
        <SendIcon />
      </div>
      {
        isLoading ? (
          <div>
            <h3>Analyzing...</h3>
          </div>
        ) : (<></>)
      }


    </main>
  );
};

export default Pipeline;
