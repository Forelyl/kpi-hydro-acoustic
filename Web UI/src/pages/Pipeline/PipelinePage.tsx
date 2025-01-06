import PipelineStep from './PipelineStep/PipelineStep';
import usePipeline from '../../hooks/usePipeline';
import PlusIcon from '../../components/icons/PlusIcon';
import SendIcon from '../../components/icons/SendIcon';
import { useSendPipelineMutation } from '../../store/pipelineApi';
import { useAppSelector } from '../../store/store';

const Pipeline = () => {
  const { pipeline, handleAddStep } = usePipeline();
  const [sendPipeline] = useSendPipelineMutation();
  const { file, separateTracks } = useAppSelector((state) => state.loadedFile);

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
      .then((res) => console.log(res))
      .catch(console.error);
  };

  return (
    <main id="pipline_page">
      {pipeline.map((step) => (
        <PipelineStep step={step} key={step.id} />
      ))}

      <div onClick={handleAddStep} id="add_step">
        <PlusIcon />
      </div>
      <div onClick={handleSendPipeline} id="add_step">
        <SendIcon />
      </div>
    </main>
  );
};

export default Pipeline;
