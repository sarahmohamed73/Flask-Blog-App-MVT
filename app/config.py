class Config:
  @staticmethod
  def init_app():
    pass


class DevelopmentConfig(Config):
  DEBUG=True
  SQLALCHEMY_DATABASE_URI= "sqlite:///project.sqlite"


class ProductionConfig(Config):
  DEBUG=False
  SQLALCHEMY_DATABASE_URI= "postgresql://sarah:12345@localhost:5432/blog"



projectConfig={
  "dev": DevelopmentConfig,
  'prd': ProductionConfig
}