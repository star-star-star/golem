from PyQt4 import QtCore

from MainWindow import GNRMainWindow

from TaskTableElem import TaskTableElem

class UiCustomizer:
    ####################
    def __init__( self, gui, logic ):

        assert isinstance( gui, GNRMainWindow )

        self.gui    = gui
        self.logic  = logic
        QtCore.QObject.connect( self.gui, QtCore.SIGNAL("taskTableRowClicked(int)"), self.__taskTableRowClicked )

    ####################
    # Add new task to golem client
    def enqueueNewTask( self, uiNewTaskInfo ):
        self.logic.enqueueNewTask( uiNewTaskInfo )

    ####################
    # Updates tasks information in gui
    def updateTasks( self, tasks ):
        for i in range( self.gui.ui.renderTaskTableWidget.rowCount() ):
            taskID = self.gui.ui.renderTaskTableWidget.item( i, 0 ).text()
            taskID = "{}".format( taskID )
            if taskID in tasks:
                self.gui.ui.renderTaskTableWidget.item( i, 1 ).setText( tasks[ taskID ].status )
                progressBarInBoxLayout = self.gui.ui.renderTaskTableWidget.cellWidget( i, 2 )
                layout = progressBarInBoxLayout.layout()
                pb = layout.itemAt( 0 ).widget()
                pb.setProperty( "value", int( tasks[ taskID ].progress * 100.0 ) )
            else:
                assert False, "Trying to update not added task."
        
    ####################
    # Add task information in gui
    def addTask( self, task ):
        self.__addTask( task.id, task.status )

    ####################
    def updateTaskAdditionalInfo( self, id ):
        t = self.logic.getTask( id )
        from TaskStatus import TaskStatus
        assert isinstance( t, TaskStatus )

        self.gui.ui.minNodePower.setText( "{} ray per pixel".format( t.minPower ) )
        self.gui.ui.minSubtask.setText( "{} pixels".format( t.minSubtask ) )
        self.gui.ui.maxSubtask.setText( "{} pixels".format( t.maxSubtask ) )
        self.gui.ui.subtaskTimeout.setText( "{} minutes".format( int( t.minSubtask / 60.0 ) ) )
        self.gui.ui.resolution.setText( "{} x {}".format( t.resolution[ 0 ], t.resolution[ 1 ] ) )
        self.gui.ui.renderer.setText( "{}".format( t.renderer ) )
        self.gui.ui.algorithType.setText( "{}".format( t.algorithmType ) )
        self.gui.ui.pixelFilter.setText( "{}".format( t.pixelFilter ) )
        self.gui.ui.samplesPerPixel.setText( "{}".format( t.samplesPerPixelCount ) )
        self.gui.ui.outputFile.setText( "{}".format( t.outputFile ) )
        self.gui.ui.fullTaskTimeout.setText( "{}".format( t.fullTaskTimeout ) )
        self.gui.ui.timeStarted.setText( "{}".format( t.timeStarted ) )

    ############################
    def __addTask( self, id, status ):
        currentRowCount = self.gui.ui.renderTaskTableWidget.rowCount()
        self.gui.ui.renderTaskTableWidget.insertRow( currentRowCount )

        taskTableElem = TaskTableElem( id, status )

        for col in range( 0, 2 ): self.gui.ui.renderTaskTableWidget.setItem( currentRowCount, col, taskTableElem.getColumnItem( col ) )

        self.gui.ui.renderTaskTableWidget.setCellWidget( currentRowCount, 2, taskTableElem.progressBarInBoxLayoutWidget )


    # SLOTS

    #############################
    def __taskTableRowClicked( self, row ):
        if row < self.gui.ui.renderTaskTableWidget.rowCount():
            taskId = self.gui.ui.renderTaskTableWidget.item( row, 0 ).text()
            taskId = "{}".format( taskId )
            self.updateTaskAdditionalInfo( taskId )
