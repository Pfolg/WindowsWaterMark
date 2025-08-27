#include "widget.h"
#include <QMessageBox>
#include "doconfig.h"
#include <QDebug>

Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    QCoreApplication *coreapp = QCoreApplication::instance();
    QApplication *app = qobject_cast<QApplication *>(coreapp);
    QScreen *screen = app->primaryScreen();
    this->setGeometry(0, 0, screen->geometry().width(), screen->geometry().height());

    // 窗口顶置，去标题栏，去除任务栏图标，鼠标穿透，窗口透明，不可聚焦
    this->setAttribute(Qt::WA_TranslucentBackground, true);
    this->setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint | Qt::ToolTip | Qt::WindowTransparentForInput | Qt::WindowDoesNotAcceptFocus);
    this->headerLabel = new QLabel(this);
    this->bodyLabel = new QLabel(this);
    // 样式
    headerLabel->setStyleSheet("background-color: rgba(0, 0, 0, 0); color: rgba(255, 255, 255, 0.5); font-size: 22px;");
    bodyLabel->setStyleSheet("background-color: rgba(0, 0, 0, 0); color: rgba(255, 255, 255, 0.5); font-size: 16px;");
    this->init();
}
void Widget::init()
{
    try
    {
        Data d = readConfig();
        this->adjustLabel(d.ratio["up"], d.ratio["down"], d.ratio["left"], d.ratio["right"]);
        this->checkSingleInstance(d.port);
        // string转QString
        qDebug() << d.line1;
        qDebug() << d.line2;
        this->headerLabel->setText(QString::fromStdString(d.line1));
        this->bodyLabel->setText(QString::fromStdString(d.line2));
    }
    catch (const std::exception &e)
    {
        qWarning() << e.what() << '\n';
        QMessageBox::critical(nullptr, "Error", "配置文件读取失败，请检查配置文件是否存在或格式是否正确。\n使用默认配置！");
        this->adjustLabel();
        this->checkSingleInstance();
        this->headerLabel->setText("激活 Windows");
        this->bodyLabel->setText("转到\"设置\"以激活 Windows。");
    }
}

Widget::~Widget()
{
}
void Widget::adjustLabel(int up, int down, int left, int right)
{
    // 清除现有布局
    if (this->layout())
    {
        delete this->layout();
    }

    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    // 上方空白 (拉伸因子 = up)
    mainLayout->addStretch(up);

    // 水平布局容器
    QHBoxLayout *hContainer = new QHBoxLayout();
    // 左侧空白 (拉伸因子 = left)
    hContainer->addStretch(left);

    // 文字容器
    QVBoxLayout *textLayout = new QVBoxLayout();
    textLayout->addWidget(headerLabel);
    textLayout->addWidget(bodyLabel);
    hContainer->addLayout(textLayout);

    // 右侧空白 (拉伸因子 = right)
    hContainer->addStretch(right);

    // 添加水平容器到主布局
    mainLayout->addLayout(hContainer);

    // 下方空白 (拉伸因子 = down)
    mainLayout->addStretch(down);

    this->setLayout(mainLayout);
}

void Widget::closeEvent(QCloseEvent *event)
{
    event->ignore();
}

void Widget::checkSingleInstance(int port)
{
    QTcpSocket *singleInstanceSocket = new QTcpSocket(this);
    singleInstanceSocket->connectToHost("127.0.0.1", port);
    if (singleInstanceSocket->waitForConnected(100))
    {
        QMessageBox::warning(nullptr, "Warning", "端口 " + QString::number(port) + " 正在使用，可能已经有实例在运行，或者更改端口。");
        exit(0);
    }
    else
    {
        QTcpServer *server = new QTcpServer(this);
        if (!server->listen(QHostAddress::LocalHost, port))
        {
            QMessageBox::critical(nullptr, "Error", "无法监听端口 " + QString::number(port));
            exit(0);
        }
    }
}