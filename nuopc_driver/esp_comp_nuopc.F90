module esp_comp_nuopc
! this is a dummy module to be used to temporarily build a dummy libesp.a

  use ESMF             , only : ESMF_VM, ESMF_VMBroadcast
  use ESMF             , only : ESMF_Mesh, ESMF_GridComp, ESMF_SUCCESS, ESMF_LogWrite
  use ESMF             , only : ESMF_GridCompSetEntryPoint, ESMF_METHOD_INITIALIZE
  use ESMF             , only : ESMF_MethodRemove, ESMF_State, ESMF_Clock, ESMF_TimeInterval
  use ESMF             , only : ESMF_State, ESMF_Field, ESMF_LOGMSG_INFO, ESMF_ClockGet
  use ESMF             , only : ESMF_Time, ESMF_Alarm, ESMF_TimeGet, ESMF_TimeInterval
  use ESMF             , only : operator(+), ESMF_TimeIntervalGet, ESMF_ClockGetAlarm
  use ESMF             , only : ESMF_AlarmIsRinging, ESMF_AlarmRingerOff, ESMF_StateGet
  use ESMF             , only : ESMF_FieldGet, ESMF_MAXSTR, ESMF_VMBroadcast
  use ESMF             , only : ESMF_TraceRegionEnter, ESMF_TraceRegionExit, ESMF_GridCompGet
  use ESMF             , only : ESMF_KIND_R8, ESMF_LogFoundError
  use ESMF             , only : ESMF_LOGERR_PASSTHRU, ESMF_LOGWRITE
  use NUOPC            , only : NUOPC_CompDerive, NUOPC_CompSetEntryPoint, NUOPC_CompSpecialize
  use NUOPC            , only : NUOPC_CompAttributeGet, NUOPC_Advertise
  use NUOPC            , only : NUOPC_CompFilterPhaseMap
  use NUOPC_Model      , only : model_routine_SS        => SetServices
  use NUOPC_Model      , only : model_label_Advance     => label_Advance
  use NUOPC_Model      , only : model_label_SetRunClock => label_SetRunClock
  use NUOPC_Model      , only : model_label_Finalize    => label_Finalize
  use NUOPC_Model      , only : NUOPC_ModelGet, setVM

  implicit none
  private ! except

  public  :: SetServices
  public  :: SetVM

  character(len=*),parameter :: u_FILE_u = &
     __FILE__

  contains

  subroutine SetServices(gcomp, rc)
    type(ESMF_GridComp)  :: gcomp
    integer, intent(out) :: rc

    ! local variables
    character(len=*),parameter  :: subname='(DART_cap:SetServices)'

    rc = ESMF_SUCCESS
    call ESMF_LogWrite(subname//' called', ESMF_LOGMSG_INFO)

    ! the NUOPC gcomp component will register the generic methods
    call NUOPC_CompDerive(gcomp, model_routine_SS, rc=rc)
    if (ChkErr(rc,__LINE__,u_FILE_u)) return

    ! switching to IPD versions
    call ESMF_GridCompSetEntryPoint(gcomp, ESMF_METHOD_INITIALIZE, &
        userRoutine=InitializeP0, phase=0, rc=rc)
    if (ChkErr(rc,__LINE__,u_FILE_u)) return

    ! set entry point for methods that require specific implementation
    call NUOPC_CompSetEntryPoint(gcomp, ESMF_METHOD_INITIALIZE, &
      phaseLabelList=(/"IPDv03p1"/), userRoutine=InitializeAdvertise, rc=rc)
    if (ChkErr(rc,__LINE__,u_FILE_u)) return
    call NUOPC_CompSetEntryPoint(gcomp, ESMF_METHOD_INITIALIZE, &
      phaseLabelList=(/"IPDv03p3"/), userRoutine=InitializeRealize, rc=rc)
    if (ChkErr(rc,__LINE__,u_FILE_u)) return

  end subroutine SetServices

  subroutine InitializeP0(gcomp, importState, exportState, clock, rc)
    type(ESMF_GridComp)   :: gcomp                    !< ESMF_GridComp object
    type(ESMF_State)      :: importState, exportState !< ESMF_State object for
                                                      !! import/export fields
    type(ESMF_Clock)      :: clock                    !< ESMF_Clock object
    integer, intent(out)  :: rc                       !< return code

    rc = ESMF_SUCCESS

    ! Switch to IPDv03 by filtering all other phaseMap entries
    call NUOPC_CompFilterPhaseMap(gcomp, ESMF_METHOD_INITIALIZE, &
         acceptStringList=(/"IPDv03p"/), rc=rc)
    if (ChkErr(rc,__LINE__,u_FILE_u)) return
  end subroutine InitializeP0

  subroutine InitializeAdvertise(gcomp, importState, exportState, clock, rc)
    type(ESMF_GridComp)            :: gcomp                    !< ESMF_GridComp object
    type(ESMF_State)               :: importState, exportState !< ESMF_State object for
                                                               !! import/export fields
    type(ESMF_Clock)               :: clock                    !< ESMF_Clock object
    integer, intent(out)           :: rc                       !< return code

    rc = ESMF_SUCCESS
  end subroutine InitializeAdvertise

  subroutine InitializeRealize(gcomp, importState, exportState, clock, rc)
    type(ESMF_GridComp)  :: gcomp                    !< ESMF_GridComp object
    type(ESMF_State)     :: importState, exportState !< ESMF_State object for
                                                     !! import/export fields
    type(ESMF_Clock)     :: clock                    !< ESMF_Clock object
    integer, intent(out) :: rc                       !< return code

    rc = ESMF_SUCCESS
  end subroutine InitializeRealize

!> Returns true if ESMF_LogFoundError() determines that rc is an error code. Otherwise false.
logical function ChkErr(rc, line, file)
  integer, intent(in) :: rc            !< return code to check
  integer, intent(in) :: line          !< Integer source line number
  character(len=*), intent(in) :: file !< User-provided source file name
  integer :: lrc
  ChkErr = .false.
  lrc = rc
  if (ESMF_LogFoundError(rcToCheck=lrc, msg=ESMF_LOGERR_PASSTHRU, line=line, file=file)) then
    ChkErr = .true.
  endif
end function ChkErr

end module esp_comp_nuopc