#ifndef WIDGET_H
#define WIDGET_H
#include <QCoreApplication>
#include <QWidget>
#include <QApplication>
#include <QScreen>
#include <QLabel>
#include <QVBoxLayout>
#include <QCloseEvent>
#include <QtNetwork/QTcpSocket>
#include <QtNetwork/QTcpServer>
#include <QString>

QT_BEGIN_NAMESPACE
namespace Ui
{
    class Widget;
}
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();
    QLabel *headerLabel;
    QLabel *bodyLabel;
    void adjustLabel(int up = 8, int down = 1, int left = 20, int right = 1);
    void closeEvent(QCloseEvent *event);
    void checkSingleInstance(int port = 20520);
    void init();

private slots:
};
#endif // WIDGET_H
