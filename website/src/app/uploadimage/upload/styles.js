export const styles = `
  .upload-container {
    background-color: rgba(255, 255, 255, 1);
    display: flex;
    padding-bottom: 103px;
    flex-direction: column;
    overflow: hidden;
  }
  .header {
    background-color: rgba(165, 157, 132, 1);
    display: flex;
    align-items: flex-start;
    gap: 10px;
    color: rgba(255, 255, 255, 1);
    flex-wrap: wrap;
    padding: 15px 17px 29px;
    font: 700 48px Montserrat, -apple-system, Roboto, Helvetica, sans-serif;
  }
  .logo {
    aspect-ratio: 1.33;
    object-fit: contain;
    object-position: center;
    width: 133px;
    align-self: start;
    max-width: 100%;
  }
  .site-title {
    flex-grow: 1;
    width: 1236px;
    flex-basis: auto;
    margin: auto 0;
  }
  .content-wrapper {
    border-radius: 28px;
    background-color: rgba(215, 211, 191, 1);
    align-self: center;
    display: flex;
    margin-top: 117px;
    width: 1200px;
    max-width: 100%;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 75px 80px;
    border: 2px solid rgba(0, 0, 0, 1);
  }
  .upload-section {
    display: flex;
    margin-left: 27px;
    width: 823px;
    max-width: 100%;
    flex-direction: column;
    align-items: center;
  }
  .section-title {
    color: rgba(0, 0, 0, 1);
    align-self: stretch;
    font: 700 40px Inter, sans-serif;
  }
  .options-container {
    margin-top: 57px;
    width: 655px;
    max-width: 100%;
  }
  .options-grid {
    gap: 20px;
    display: flex;
  }
  .upload-option {
    border-radius: 28px;
    background-color: rgba(193, 186, 161, 1);
    display: flex;
    flex-direction: column;
    color: rgba(255, 255, 255, 1);
    width: 100%;
    padding: 22px 26px 22px 60px;
    font: 700 36px Inter, sans-serif;
  }
  .option-icon {
    aspect-ratio: 1;
    object-fit: contain;
    object-position: center;
    width: 200px;
  }
  .option-label {
    align-self: center;
    margin-top: 13px;
  }
  .next-button {
    border-radius: 28px;
    background-color: rgba(215, 211, 191, 1);
    margin-top: 45px;
    width: 315px;
    max-width: 100%;
    color: rgba(0, 0, 0, 1);
    padding: 12px 70px 26px;
    font: 400 32px Inter, sans-serif;
    border: 2px solid rgba(0, 0, 0, 1);
    cursor: pointer;
  }
  @media (max-width: 991px) {
    .upload-container {
      padding-bottom: 100px;
    }
    .header {
      font-size: 40px;
    }
    .site-title {
      max-width: 100%;
      font-size: 40px;
    }
    .content-wrapper {
      margin-top: 40px;
      padding: 0 20px;
    }
    .options-container {
      margin-top: 40px;
    }
    .options-grid {
      flex-direction: column;
      align-items: stretch;
      gap: 0px;
    }
    .upload-option {
      margin-top: 40px;
      padding: 0 20px;
    }
    .next-button {
      margin-top: 40px;
      padding: 0 20px;
    }
  }
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
`;
