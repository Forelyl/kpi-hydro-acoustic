import { useLocation, useNavigate, Link} from 'react-router';
import CloseIcon from '../icons/CloseIcon';
import HeaderNavigation from './HeaderNavigation';

const Header = () => {
  const { pathname } = useLocation();
  const navigate = useNavigate();

  const handleGoBack = () => {
    const promise = navigate(-1);
    if (promise) promise.catch(console.error);
  };

  return (
    <header>
      <Link to="/" draggable="false"><img src="logo.svg" draggable="false"/></Link>
      <h1>
        <span>Sound</span>
        <span className="green_text">Surface</span>
      </h1>
      {pathname === '/about' ? (
        <div onClick={handleGoBack} id="close_button">
          <CloseIcon />
        </div>
      ) : (
        <HeaderNavigation />
      )}
    </header>
  );
};

export default Header;
