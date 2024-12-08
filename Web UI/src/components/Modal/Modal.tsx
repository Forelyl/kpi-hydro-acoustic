import { PropsWithChildren } from 'react';
import styles from './Modal.module.css';

interface Props {
  open: boolean;
}

const Modal = ({ children, open }: PropsWithChildren<Props>) => {
  if (open)
    return (
      <div className={styles.modal}>
        <div className={styles['modal-wrapper']}>
          <div className={styles['modal-content']}>{children}</div>
        </div>
      </div>
    );
};

export default Modal;
